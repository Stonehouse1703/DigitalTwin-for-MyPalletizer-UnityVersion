using System;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;

public class WorldUdpBridge : MonoBehaviour
{
    [Header("Networking")]
    public int port = 5006;

    [Header("References")]
    public WorldSpawnManager spawnManager;

    private UdpClient _udpClient;
    private Thread _receiveThread;
    private volatile bool _running = true;

    private readonly Queue<WorldMessage> _messageQueue = new();
    private readonly object _lock = new();

    void Start()
    {
        if (spawnManager == null)
        {
            spawnManager = FindFirstObjectByType<WorldSpawnManager>();
        }

        if (spawnManager == null)
        {
            Debug.LogError("WorldUdpBridge: No WorldSpawnManager found in scene.");
            enabled = false;
            return;
        }

        _receiveThread = new Thread(ReceiveData) { IsBackground = true };
        _receiveThread.Start();

        Debug.Log($"World UDP Bridge started on port {port}");
    }

    void Update()
    {
        while (true)
        {
            WorldMessage msg = null;

            lock (_lock)
            {
                if (_messageQueue.Count > 0)
                {
                    msg = _messageQueue.Dequeue();
                }
            }

            if (msg == null)
                break;

            spawnManager.HandleMessage(msg);
        }
    }

    private void ReceiveData()
    {
        try
        {
            _udpClient = new UdpClient(port);

            while (_running)
            {
                try
                {
                    IPEndPoint anyIP = new IPEndPoint(IPAddress.Any, 0);
                    byte[] data = _udpClient.Receive(ref anyIP);
                    string text = Encoding.UTF8.GetString(data);

                    WorldMessage msg = JsonUtility.FromJson<WorldMessage>(text);
                    if (msg == null || string.IsNullOrWhiteSpace(msg.type))
                    {
                        Debug.LogWarning("WorldUdpBridge: Received invalid JSON.");
                        continue;
                    }

                    lock (_lock)
                    {
                        _messageQueue.Enqueue(msg);
                    }

                    Debug.Log($"World command enqueued: {msg.type}");
                }
                catch (SocketException)
                {
                    // normal beim Shutdown
                }
                catch (Exception e)
                {
                    Debug.LogWarning("World UDP Receive Error: " + e.Message);
                }
            }
        }
        catch (Exception e)
        {
            Debug.LogError("WorldUdpBridge startup failed: " + e.Message);
        }
    }

    private void OnApplicationQuit()
    {
        _running = false;
        _udpClient?.Close();
        _receiveThread?.Join(200);
    }
}