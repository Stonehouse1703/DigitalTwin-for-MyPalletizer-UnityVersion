using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class CameraViewManager : MonoBehaviour
{
    [System.Serializable]
    public class CameraView
    {
        public string name;
        public Transform viewTransform;
        public bool orthographic = false;
        public float orthographicSize = 0.5f;
    }

    [Header("References")]
    public Camera targetCamera;
    public TMP_Dropdown dropdown;

    [Header("Views")]
    public List<CameraView> views = new();

    [Header("Behavior")]
    public bool instantSwitch = true;
    public float smoothSpeed = 5f;

    private CameraView _currentView;

    void Start()
    {
        if (targetCamera == null)
            targetCamera = Camera.main;

        if (dropdown != null)
        {
            dropdown.ClearOptions();

            List<string> names = new();
            foreach (var view in views)
            {
                names.Add(view.name);
            }

            dropdown.AddOptions(names);
            dropdown.onValueChanged.AddListener(SetViewByIndex);
        }

        if (views.Count > 0)
        {
            ApplyView(views[0], true);
            if (dropdown != null)
                dropdown.value = 0;
        }
    }

    void Update()
    {
        if (instantSwitch || _currentView == null || _currentView.viewTransform == null)
            return;

        targetCamera.transform.position = Vector3.Lerp(
            targetCamera.transform.position,
            _currentView.viewTransform.position,
            Time.deltaTime * smoothSpeed
        );

        targetCamera.transform.rotation = Quaternion.Slerp(
            targetCamera.transform.rotation,
            _currentView.viewTransform.rotation,
            Time.deltaTime * smoothSpeed
        );

        if (_currentView.orthographic)
        {
            targetCamera.orthographic = true;
            targetCamera.orthographicSize = Mathf.Lerp(
                targetCamera.orthographicSize,
                _currentView.orthographicSize,
                Time.deltaTime * smoothSpeed
            );
        }
        else
        {
            targetCamera.orthographic = false;
        }
    }

    public void SetViewByIndex(int index)
    {
        if (index < 0 || index >= views.Count)
            return;

        ApplyView(views[index], instantSwitch);
    }

    private void ApplyView(CameraView view, bool immediate)
    {
        if (view == null || view.viewTransform == null || targetCamera == null)
            return;

        _currentView = view;

        if (immediate)
        {
            targetCamera.transform.position = view.viewTransform.position;
            targetCamera.transform.rotation = view.viewTransform.rotation;
        }

        targetCamera.orthographic = view.orthographic;
        if (view.orthographic)
        {
            targetCamera.orthographicSize = view.orthographicSize;
        }
    }
}