using UnityEngine;

public class RobotToolManager : MonoBehaviour
{
    [Header("Tool Roots")]
    public GameObject gripperTool;
    public GameObject pumpTool;

    [Header("Optional Logic Components")]
    public SimpleGripperController gripperController;
    public SuctionPumpController pumpController;

    public string CurrentTool { get; private set; } = "gripper";

    void Start()
    {
        SetTool(CurrentTool);
    }

    public void SetTool(string tool)
    {
        tool = (tool ?? "").Trim().ToLower();

        if (tool != "gripper" && tool != "pump")
        {
            Debug.LogWarning($"Unknown tool '{tool}'");
            return;
        }

        CurrentTool = tool;

        if (gripperTool != null)
            gripperTool.SetActive(tool == "gripper");

        if (pumpTool != null)
            pumpTool.SetActive(tool == "pump");

        Debug.Log($"Active end effector set to: {tool}");
    }

    public void SetGripperState(int flag, int speed, int type1 = 1)
    {
        if (CurrentTool != "gripper")
        {
            Debug.LogWarning("Gripper command ignored because current tool is not 'gripper'.");
            return;
        }

        if (gripperController == null)
        {
            Debug.LogWarning("No SimpleGripperController assigned.");
            return;
        }

        gripperController.SetGripperState(flag, speed, type1);
    }

    public void SetPump(bool enabled)
    {
        if (CurrentTool != "pump")
        {
            Debug.LogWarning("Pump command ignored because current tool is not 'pump'.");
            return;
        }

        if (pumpController == null)
        {
            Debug.LogWarning("No SuctionPumpController assigned.");
            return;
        }

        if (enabled) pumpController.PumpOn();
        else pumpController.PumpOff();
    }
}