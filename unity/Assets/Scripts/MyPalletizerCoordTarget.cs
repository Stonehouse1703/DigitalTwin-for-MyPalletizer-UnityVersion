using UnityEngine;

public class MyPalletizerCoordTarget : MonoBehaviour
{
    [Header("Target transform that represents the desired TCP pose")]
    public Transform target;

    [Header("Unit conversion")]
    [Tooltip("If your scene is in meters: set 0.001 (mm -> m). If in mm: set 1.0.")]
    public float positionScale = 0.001f;

    [Header("Defaults")]
    public float currentX, currentY, currentZ, currentRx;
    
    public MyPalletizerArticulationAdapter adapter;
    public MyPalletizerIKSolver ik;

    private void Awake()
    {
        if (target == null) target = transform;
        if (adapter == null) adapter = FindFirstObjectByType<MyPalletizerArticulationAdapter>();
        if (ik == null) ik = FindFirstObjectByType<MyPalletizerIKSolver>();
    }

    // coord_id: 1=x,2=y,3=z,4=rx
    public void ApplySingleCoord(int coordId, float coord, float speed)
    {
        switch (coordId)
        {
            case 1: currentX = coord; break;
            case 2: currentY = coord; break;
            case 3: currentZ = coord; break;
            case 4: currentRx = coord; break;
            default:
                Debug.LogWarning($"Invalid coord_id {coordId} (expected 1..4)");
                return;
        }

        ApplyCoords(currentX, currentY, currentZ, currentRx, speed);
    }

    public void ApplyCoords(float x, float y, float z, float rx, float speed)
    {
        currentX = x; currentY = y; currentZ = z; currentRx = rx;

        // Apply as target pose (best-effort).
        // NOTE: This does NOT move the robot joints unless you have IK that consumes this target.
        var pos = new Vector3(x, y, z) * positionScale;
        target.localPosition = pos;

        // rx is typically rotation around X in degrees (depending on your robot convention).
        target.localRotation = Quaternion.Euler(rx, 0f, 0f);

        // Hook point: call IK solver here if you have one.
        // Example:
        // ikSolver.SolveAndApply(target);
        
        if (ik != null && adapter != null)
        {
            if (ik.TrySolve(x, y, z, rx, out var a1, out var a2, out var a3, out var a4))
            {
                adapter.MoveJointsAsync(a1, a2, a3, a4, speed);
            }
        }
    }
}