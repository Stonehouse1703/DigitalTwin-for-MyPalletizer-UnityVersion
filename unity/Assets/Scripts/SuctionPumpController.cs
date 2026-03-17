using UnityEngine;

public class SuctionPumpController : MonoBehaviour
{
    [Header("Optional Visuals")]
    public GameObject pumpVisualOn;
    public GameObject pumpVisualOff;

    [Header("Pickup")]
    public Transform attachPoint;
    public float suctionRadius = 0.03f;
    public LayerMask pickupLayers = ~0;

    public bool IsOn { get; private set; }

    private GrabbableObject _attachedObject;

    public void PumpOn()
    {
        IsOn = true;
        UpdateVisuals();

        TryAttachNearestObject();

        Debug.Log("Pump ON");
    }

    public void PumpOff()
    {
        IsOn = false;
        UpdateVisuals();

        ReleaseAttachedObject();

        Debug.Log("Pump OFF");
    }

    private void TryAttachNearestObject()
    {
        if (_attachedObject != null)
            return;

        Transform refPoint = attachPoint != null ? attachPoint : transform;

        Collider[] hits = Physics.OverlapSphere(refPoint.position, suctionRadius, pickupLayers);

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
            return;

        AttachObject(best);
    }

    private void AttachObject(GrabbableObject obj)
    {
        _attachedObject = obj;

        Transform parent = attachPoint != null ? attachPoint : transform;
        obj.AttachTo(parent);

        Debug.Log($"Pump attached object: {obj.name}");
    }

    private void ReleaseAttachedObject()
    {
        if (_attachedObject == null)
            return;

        _attachedObject.Detach();
        Debug.Log($"Pump released object: {_attachedObject.name}");
        _attachedObject = null;
    }

    private void UpdateVisuals()
    {
        if (pumpVisualOn != null)
            pumpVisualOn.SetActive(IsOn);

        if (pumpVisualOff != null)
            pumpVisualOff.SetActive(!IsOn);
    }

    void OnDrawGizmosSelected()
    {
        Transform refPoint = attachPoint != null ? attachPoint : transform;
        Gizmos.color = Color.cyan;
        Gizmos.DrawWireSphere(refPoint.position, suctionRadius);
    }
}