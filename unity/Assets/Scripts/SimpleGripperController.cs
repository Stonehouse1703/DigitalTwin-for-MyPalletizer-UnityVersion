using UnityEngine;

public class SimpleGripperController : MonoBehaviour
{
    [Header("Pickup")]
    public Transform attachPoint;
    public float gripRadius = 0.04f;
    public LayerMask pickupLayers = ~0;

    private GrabbableObject _heldObject;

    public void SetGripperState(int flag, float speed, int type1 = 1)
    {
        switch (flag)
        {
            case 0:     // open
                Release();
                break;

            case 1:     // close
                TryGrip();
                break;

            case 254:   // release
                Release();
                break;

            default:
                Debug.LogWarning($"Unknown gripper flag: {flag}");
                break;
        }

        Debug.Log($"SimpleGripperController -> flag={flag}, speed={speed}, type1={type1}");
    }

    public void TryGrip()
    {
        if (_heldObject != null)
        {
            Debug.Log("Already holding an object.");
            return;
        }

        Transform refPoint = attachPoint != null ? attachPoint : transform;

        Collider[] hits = Physics.OverlapSphere(refPoint.position, gripRadius, pickupLayers);

        GrabbableObject best = null;
        float bestDistance = float.MaxValue;

        foreach (Collider hit in hits)
        {
            GrabbableObject candidate = hit.GetComponentInParent<GrabbableObject>();
            if (candidate == null) continue;
            if (!candidate.canBePicked) continue;
            if (candidate.isAttached) continue;

            float d = Vector3.Distance(refPoint.position, candidate.transform.position);
            if (d < bestDistance)
            {
                bestDistance = d;
                best = candidate;
            }
        }

        if (best == null)
        {
            Debug.Log("No grabbable object found.");
            return;
        }

        Transform parent = attachPoint != null ? attachPoint : transform;
        best.AttachTo(parent);
        _heldObject = best;

        Debug.Log($"Gripped object: {best.name}");
    }

    public void Release()
    {
        if (_heldObject == null)
        {
            Debug.Log("No object to release.");
            return;
        }

        _heldObject.Detach();
        Debug.Log($"Released object: {_heldObject.name}");
        _heldObject = null;
    }

    private void OnDrawGizmosSelected()
    {
        Transform refPoint = attachPoint != null ? attachPoint : transform;
        Gizmos.color = Color.yellow;
        Gizmos.DrawWireSphere(refPoint.position, gripRadius);
    }
}