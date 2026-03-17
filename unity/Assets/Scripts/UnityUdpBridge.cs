using UnityEngine;
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Collections.Generic;

public class UnityUdpBridge : MonoBehaviour
{
    [Header("Networking")]
    public int port = 5005;

    [Header("LED Controller")]
    public RobotLEDController ledController;

    [Header("Robot Reference")]
    public MyPalletizerArticulationAdapter adapter;

	[Header("Tool Manager")]
	public RobotToolManager toolManager;

    private UdpClient _udpClient;
    private Thread _receiveThread;
    private volatile bool _running = true;

    private readonly Queue<RobotCommand> _commandQueue = new();
    private readonly object _lock = new object();

    [Serializable]
	public class RobotData
	{
    	public string type;
    	public float j1, j2, j3, j4;
    	public int speed;
    	public int r, g, b;

    	public string tool;
    	public int flag;
    	public int type_1;
    	public bool enabled;
	}

    private struct RobotCommand
	{
    	public string type;
    	public float j1, j2, j3, j4;
    	public int speed;
    	public int r, g, b;

    	public string tool;
    	public int flag;
    	public int type_1;
    	public bool enabled;
	}

    void Start()
    {
        if (adapter == null) adapter = GetComponent<MyPalletizerArticulationAdapter>();
        if (ledController == null) ledController = FindFirstObjectByType<RobotLEDController>();
		if (toolManager == null) toolManager = FindFirstObjectByType<RobotToolManager>();

        _receiveThread = new Thread(ReceiveData) { IsBackground = true };
        _receiveThread.Start();

        StartCoroutine(CommandRunner());

        Debug.Log($"UDP Bridge gestartet auf Port {port}");
    }

    private void ReceiveData()
    {
        _udpClient = new UdpClient(port);

        while (_running)
        {
            try
            {
                IPEndPoint anyIP = new IPEndPoint(IPAddress.Any, 0);
                byte[] data = _udpClient.Receive(ref anyIP); // blockiert
                string text = Encoding.UTF8.GetString(data);

                var robotData = JsonUtility.FromJson<RobotData>(text);
                if (robotData == null || string.IsNullOrWhiteSpace(robotData.type))
                    continue;

                lock (_lock)
                {
                    _commandQueue.Enqueue(new RobotCommand
					{
                        type = robotData.type,
                        j1 = robotData.j1,
                        j2 = robotData.j2,
                        j3 = robotData.j3,
                        j4 = robotData.j4,
                        speed = robotData.speed,
                        r = robotData.r,
                        g = robotData.g,
                        b = robotData.b,
                        tool = robotData.tool,
                        flag = robotData.flag,
                        type_1 = robotData.type_1,
                        enabled = robotData.enabled
                    });
                    Debug.Log("Enqueued command: " + robotData.type);
                }
            }
            catch (SocketException)
            {
                // tritt beim Close() auf -> ok beim Shutdown
            }
            catch (Exception e)
            {
                Debug.LogWarning("UDP Receive Error: " + e.Message);
            }
        }
    }

    private System.Collections.IEnumerator CommandRunner()
    {
        while (_running)
        {
            RobotCommand cmd;
            bool hasCmd = false;

            lock (_lock)
            {
                if (_commandQueue.Count > 0)
                {
                    cmd = _commandQueue.Dequeue();
                    hasCmd = true;
                }
                else cmd = default;
            }

            if (!hasCmd)
            {
                yield return null;
                continue;
            }

            Debug.Log("Received command: " + cmd.type + ", j1=" + cmd.j1 + ", j2=" + cmd.j2 + ", j3=" + cmd.j3 + ", j4=" + cmd.j4 + ", speed=" + cmd.speed + ", r=" + cmd.r + ", g=" + cmd.g + ", b=" + cmd.b);
            switch (cmd.type)
            {
                case "led":
                    if (ledController != null) ledController.SetLEDColor(cmd.r, cmd.g, cmd.b);
                    else Debug.LogWarning("No RobotLEDController found in scene!");
                    break;

                case "move_joints":
                    // fire & forget
                    adapter.MoveJointsAsync(cmd.j1, cmd.j2, cmd.j3, cmd.j4, cmd.speed);
                    break;

                case "sync_move_joints":
                    // blockiert die Queue bis fertig
                    yield return adapter.MoveJointsSync(cmd.j1, cmd.j2, cmd.j3, cmd.j4, cmd.speed);
                    break;
				
				case "set_end_effector":
                    if (toolManager != null)
                        toolManager.SetTool(cmd.tool);
                    else
                        Debug.LogWarning("No RobotToolManager found!");
                    break;
                
                case "set_gripper_state":
                    if (toolManager != null)
                        toolManager.SetGripperState(cmd.flag, cmd.speed, cmd.type_1);
                    else
                        Debug.LogWarning("No RobotToolManager found!");
                    break;
                
                case "pump":
                    if (toolManager != null)
                        toolManager.SetPump(cmd.enabled);
                    else
                        Debug.LogWarning("No RobotToolManager found!");
                    break;

                default:
                    Debug.LogWarning($"Unknown command type: '{cmd.type}'");
                    break;
            }
            Debug.Log("🏁 Done with command: " + cmd.type);
        }
    }

    private void OnApplicationQuit()
    {
        _running = false;
        _udpClient?.Close();       // löst Receive() auf -> Thread endet
        _receiveThread?.Join(200); // kurz warten statt Abort
    }
}