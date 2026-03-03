using UnityEngine;

public class MyPalletizerIKSolver : MonoBehaviour
{
    [Header("Robot Root (coordinate frame)")]
    public Transform robotRoot;

    [Header("Pivots / Reference points")]
    public Transform j2Pivot;   // shoulder pivot transform
    public Transform j3Pivot;   // elbow pivot transform
    public Transform tcp;       // tool center point transform (end effector)

    [Header("Units")]
    [Tooltip("If coords are in mm (typical robot), use 0.001 to convert mm->m")]
    public float mmToM = 0.001f;

    [Header("Joint angle offsets (deg)")]
    [Tooltip("Use these if IK angles are systematically shifted vs your joint zero positions.")]
    public float j1OffsetDeg = 0f;
    public float j2OffsetDeg = 0f;
    public float j3OffsetDeg = 0f;
    public float j4OffsetDeg = 0f;

    [Header("Joint limits (deg) - match your controller")]
    public float j1Min = -160f, j1Max = 160f;
    public float j2Min = 0f,    j2Max = 90f;
    public float j3Min = -60f,  j3Max = 0f;
    public float j4Min = -360f, j4Max = 360f;

    [Header("IK options")]
    public bool elbowUp = true;            // choose elbow configuration
    public float reachEps = 1e-5f;

    float L1; // shoulder -> elbow
    float L2; // elbow -> tcp

    void Awake()
    {
        if (robotRoot == null) robotRoot = transform;

        // compute link lengths from current model
        // (works if hierarchy positions are correct in rest pose)
        Vector3 p2 = robotRoot.InverseTransformPoint(j2Pivot.position);
        Vector3 p3 = robotRoot.InverseTransformPoint(j3Pivot.position);
        Vector3 pt = robotRoot.InverseTransformPoint(tcp.position);

        L1 = Vector3.Distance(p2, p3);
        L2 = Vector3.Distance(p3, pt);

        if (L1 < reachEps || L2 < reachEps)
            Debug.LogWarning($"IK link lengths suspicious. L1={L1}, L2={L2}. Check pivot assignments.");
    }

    /// <summary>
    /// Solve IK for coords [x,y,z,rx]. x,y,z in mm (typical), rx in deg.
    /// Returns joint angles in degrees suitable for your XDrive targets.
    /// </summary>
    public bool TrySolve(float xMm, float yMm, float zMm, float rxDeg,
                         out float j1Deg, out float j2Deg, out float j3Deg, out float j4Deg)
    {
        j1Deg = j2Deg = j3Deg = j4Deg = 0f;

        if (robotRoot == null || j2Pivot == null || j3Pivot == null || tcp == null)
            return false;

        // Target in robotRoot local space (meters)
        Vector3 target = new Vector3(xMm, yMm, zMm) * mmToM;

        // Shoulder pivot in robotRoot local space
        Vector3 p2 = robotRoot.InverseTransformPoint(j2Pivot.position);

        // Relative to shoulder
        Vector3 t = target - p2;

        // 1) Base yaw (j1): rotate towards target in XY plane
        // Assumption: +X forward, +Y left, +Z up in robotRoot local.
        float yawRad = Mathf.Atan2(t.y, t.x);
        j1Deg = Mathf.Rad2Deg * yawRad + j1OffsetDeg;
        j1Deg = Clamp(j1Deg, j1Min, j1Max);

        // 2) Reduce to 2D plane by projecting into radial distance r and height z
        float r = Mathf.Sqrt(t.x * t.x + t.y * t.y); // distance from base axis
        float z = t.z;

        // 3) 2-link IK for (r, z)
        float d = Mathf.Sqrt(r * r + z * z); // distance shoulder->target in that plane

        // reachable clamp (avoid NaNs)
        float maxReach = L1 + L2;
        float minReach = Mathf.Abs(L1 - L2);
        if (d > maxReach) d = maxReach;
        if (d < minReach) d = minReach;

        // Law of cosines
        float cosElbow = (L1 * L1 + L2 * L2 - d * d) / (2f * L1 * L2);
        cosElbow = Mathf.Clamp(cosElbow, -1f, 1f);
        float elbowInner = Mathf.Acos(cosElbow); // 0..pi

        // Common robotics convention: elbow angle sign depends on configuration
        float j3Rad = elbowUp ? -(Mathf.PI - elbowInner) : +(Mathf.PI - elbowInner);

        float cosShoulder = (L1 * L1 + d * d - L2 * L2) / (2f * L1 * d);
        cosShoulder = Mathf.Clamp(cosShoulder, -1f, 1f);
        float shoulderInner = Mathf.Acos(cosShoulder);

        float toTarget = Mathf.Atan2(z, r);
        float j2Rad = elbowUp ? (toTarget + shoulderInner) : (toTarget - shoulderInner);

        j2Deg = Mathf.Rad2Deg * j2Rad + j2OffsetDeg;
        j3Deg = Mathf.Rad2Deg * j3Rad + j3OffsetDeg;

        // clamp to your joint limits
        j2Deg = Clamp(j2Deg, j2Min, j2Max);
        j3Deg = Clamp(j3Deg, j3Min, j3Max);

        // 4) Wrist (j4): simplest mapping = rx
        j4Deg = rxDeg + j4OffsetDeg;
        j4Deg = Clamp(j4Deg, j4Min, j4Max);

        return true;
    }

    static float Clamp(float v, float lo, float hi) => (v < lo) ? lo : (v > hi) ? hi : v;
}