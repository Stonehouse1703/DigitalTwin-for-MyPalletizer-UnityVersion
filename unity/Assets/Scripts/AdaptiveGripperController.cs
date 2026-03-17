using UnityEngine;

public class AdaptiveGripperController : MonoBehaviour
{
    [Header("Optional Visual Parts")]
    public Transform leftFinger;
    public Transform rightFinger;

    [Header("Simple Visual Animation")]
    public float openOffset = 0.02f;
    public float closedOffset = 0.0f;

    private int _currentFlag = 0;

    public void SetGripperState(int flag, float speed, int type1 = 1)
    {
        _currentFlag = flag;

        switch (flag)
        {
            case 0:
                Open();
                break;

            case 1:
                Close();
                break;

            case 254:
                Release();
                break;

            default:
                Debug.LogWarning($"Unknown gripper flag: {flag}");
                break;
        }

        Debug.Log($"Gripper state set: flag={flag}, speed={speed}, type1={type1}");
    }

    private void Open()
    {
        SetFingerVisual(openOffset);
    }

    private void Close()
    {
        SetFingerVisual(closedOffset);
    }

    private void Release()
    {
        SetFingerVisual(openOffset);
    }

    private void SetFingerVisual(float offset)
    {
        if (leftFinger != null)
        {
            Vector3 p = leftFinger.localPosition;
            p.x = -offset;
            leftFinger.localPosition = p;
        }

        if (rightFinger != null)
        {
            Vector3 p = rightFinger.localPosition;
            p.x = offset;
            rightFinger.localPosition = p;
        }
    }
}