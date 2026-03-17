using UnityEngine;

[RequireComponent(typeof(Collider))]
public class GrabbableObject : MonoBehaviour
{
    [Header("Pickup")]
    public bool canBePicked = true;
    public Transform pickupAnchor;

    [HideInInspector]
    public bool isAttached = false;

    private Rigidbody _rb;

    void Awake()
    {
        _rb = GetComponent<Rigidbody>();
    }

    public Transform GetPickupAnchor()
    {
        return pickupAnchor != null ? pickupAnchor : transform;
    }

    public void AttachTo(Transform parent)
    {
        isAttached = true;

        if (_rb != null)
        {
            _rb.linearVelocity = Vector3.zero;
            _rb.angularVelocity = Vector3.zero;
            _rb.isKinematic = true;
            _rb.useGravity = false;
        }

        transform.SetParent(parent, true);
    }

    public void Detach()
    {
        isAttached = false;

        transform.SetParent(null, true);

        if (_rb != null)
        {
            _rb.isKinematic = false;
            _rb.useGravity = true;
        }
    }
}