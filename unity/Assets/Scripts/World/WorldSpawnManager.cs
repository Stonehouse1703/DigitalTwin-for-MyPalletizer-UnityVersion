using System.Collections.Generic;
using UnityEngine;

public class WorldSpawnManager : MonoBehaviour
{
    [Header("Prefabs")]
    public GameObject boxPrefab;
    public GameObject spherePrefab;
    public GameObject cylinderPrefab;

    [Header("Optional Parent")]
    public Transform spawnedObjectsParent;

    private readonly Dictionary<string, GameObject> _spawnedObjects = new();

    public void HandleMessage(WorldMessage msg)
    {
        if (msg == null || string.IsNullOrWhiteSpace(msg.type))
        {
            Debug.LogWarning("WorldSpawnManager received invalid message.");
            return;
        }

        switch (msg.type)
        {
            case "spawn":
                SpawnObject(msg);
                break;

            case "delete":
                DeleteObject(msg.name);
                break;

            case "clear":
                ClearAll();
                break;

            default:
                Debug.LogWarning($"Unknown world command type: '{msg.type}'");
                break;
        }
    }

    private void SpawnObject(WorldMessage msg)
    {
        if (string.IsNullOrWhiteSpace(msg.object_type))
        {
            Debug.LogWarning("Spawn failed: object_type missing.");
            return;
        }

        if (string.IsNullOrWhiteSpace(msg.name))
        {
            Debug.LogWarning("Spawn failed: name missing.");
            return;
        }

        GameObject prefab = GetPrefabByType(msg.object_type);
        if (prefab == null)
        {
            Debug.LogWarning($"Spawn failed: no prefab mapped for object_type '{msg.object_type}'");
            return;
        }

        // Falls Name schon existiert: altes löschen und neu spawnen
        if (_spawnedObjects.TryGetValue(msg.name, out var existing) && existing != null)
        {
            Destroy(existing);
            _spawnedObjects.Remove(msg.name);
        }

        Vector3 position = ToVector3(msg.position, Vector3.zero);
        Vector3 rotationEuler = ToVector3(msg.rotation, Vector3.zero);
        Vector3 scale = ToVector3(msg.scale, Vector3.one);

        GameObject go = Instantiate(
            prefab,
            position,
            Quaternion.Euler(rotationEuler),
            spawnedObjectsParent
        );
        
        if (go.GetComponent<Rigidbody>() == null)
        {
            Rigidbody rb = go.AddComponent<Rigidbody>();
            rb.mass = 0.05f;
        }

        if (go.GetComponent<GrabbableObject>() == null)
        {
            go.AddComponent<GrabbableObject>();
        }

        go.name = msg.name;
        go.transform.localScale = scale;

        ApplyColor(go, msg.color);

        _spawnedObjects[msg.name] = go;

        Debug.Log($"Spawned '{msg.name}' of type '{msg.object_type}' at {position}");
    }

    private void DeleteObject(string objectName)
    {
        if (string.IsNullOrWhiteSpace(objectName))
        {
            Debug.LogWarning("Delete failed: name missing.");
            return;
        }

        if (_spawnedObjects.TryGetValue(objectName, out var go) && go != null)
        {
            Destroy(go);
            _spawnedObjects.Remove(objectName);
            Debug.Log($"Deleted object '{objectName}'");
        }
        else
        {
            Debug.LogWarning($"Delete skipped: object '{objectName}' not found.");
        }
    }

    public void ClearAll()
    {
        foreach (var kv in _spawnedObjects)
        {
            if (kv.Value != null)
            {
                Destroy(kv.Value);
            }
        }

        _spawnedObjects.Clear();
        Debug.Log("Cleared all spawned objects.");
    }

    private GameObject GetPrefabByType(string objectType)
    {
        return objectType switch
        {
            "box" => boxPrefab,
            "sphere" => spherePrefab,
            "cylinder" => cylinderPrefab,
            _ => null
        };
    }

    private static Vector3 ToVector3(Vec3Data data, Vector3 fallback)
    {
        if (data == null) return fallback;
        return new Vector3(data.x, data.y, data.z);
    }

    private static void ApplyColor(GameObject go, ColorData colorData)
    {
        if (go == null || colorData == null) return;

        Renderer renderer = go.GetComponentInChildren<Renderer>();
        if (renderer == null) return;

        Material mat = renderer.material;
        Color color = new Color(
            Mathf.Clamp01(colorData.r / 255f),
            Mathf.Clamp01(colorData.g / 255f),
            Mathf.Clamp01(colorData.b / 255f)
        );

        mat.color = color;

        if (mat.HasProperty("_EmissionColor"))
        {
            mat.EnableKeyword("_EMISSION");
            mat.SetColor("_EmissionColor", color * 0.2f);
        }
    }
}