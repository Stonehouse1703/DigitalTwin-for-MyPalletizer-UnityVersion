using UnityEngine;

public class GripperDownConstraint : MonoBehaviour
{
    public Transform armReference;
    public Vector3 worldDownDirection = Vector3.down;
    public float headingOffsetAngle = 0f;
    [Range(0f, 1f)]
    public float strength = 1f;

    private Quaternion initialRotationOffset;
    private bool initialized = false;

    void Start()
    {
        if (armReference == null && transform.parent != null)
        {
            armReference = transform.parent;
        }

        if (armReference != null)
        {
            Vector3 targetDown = worldDownDirection.normalized;
            Vector3 referenceForward = armReference.forward;

            if (headingOffsetAngle != 0)
            {
                referenceForward = Quaternion.AngleAxis(headingOffsetAngle, targetDown) * referenceForward;
            }

            Vector3 projectedForward = Vector3.ProjectOnPlane(referenceForward, targetDown);

            if (projectedForward.sqrMagnitude < 0.001f)
            {
                projectedForward = Vector3.ProjectOnPlane(armReference.up, targetDown);
            }

            projectedForward.Normalize();

            Vector3 x = targetDown;
            Vector3 z = projectedForward;
            Vector3 y = Vector3.Cross(z, x).normalized;
            z = Vector3.Cross(x, y).normalized;

            Quaternion baseRotation = Quaternion.LookRotation(z, y);

            // Offset zwischen berechneter Zielrotation und aktueller Startrotation merken
            initialRotationOffset = Quaternion.Inverse(baseRotation) * transform.rotation;
            initialized = true;
        }
    }

    void LateUpdate()
    {
        if (armReference == null && transform.parent != null)
        {
            armReference = transform.parent;
        }

        if (armReference == null) return;

        Vector3 targetDown = worldDownDirection.normalized;
        Vector3 referenceForward = armReference.forward;

        if (headingOffsetAngle != 0)
        {
            referenceForward = Quaternion.AngleAxis(headingOffsetAngle, targetDown) * referenceForward;
        }

        Vector3 projectedForward = Vector3.ProjectOnPlane(referenceForward, targetDown);

        if (projectedForward.sqrMagnitude < 0.001f)
        {
            projectedForward = Vector3.ProjectOnPlane(armReference.up, targetDown);
        }

        projectedForward.Normalize();

        Vector3 x = targetDown;
        Vector3 z = projectedForward;
        Vector3 y = Vector3.Cross(z, x).normalized;
        z = Vector3.Cross(x, y).normalized;

        Quaternion targetRotation = Quaternion.LookRotation(z, y);

        if (initialized)
        {
            targetRotation = targetRotation * initialRotationOffset;
        }

        if (strength >= 0.999f)
        {
            transform.rotation = targetRotation;
        }
        else
        {
            transform.rotation = Quaternion.Slerp(transform.rotation, targetRotation, strength);
        }
    }
}