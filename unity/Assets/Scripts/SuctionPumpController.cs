using UnityEngine;

public class SuctionPumpController : MonoBehaviour
{
    [Header("Optional Visuals")]
    public GameObject pumpVisualOn;
    public GameObject pumpVisualOff;

    public bool IsOn { get; private set; }

    public void PumpOn()
    {
        IsOn = true;
        UpdateVisuals();
        Debug.Log("Pump ON");
    }

    public void PumpOff()
    {
        IsOn = false;
        UpdateVisuals();
        Debug.Log("Pump OFF");
    }

    private void UpdateVisuals()
    {
        if (pumpVisualOn != null)
            pumpVisualOn.SetActive(IsOn);

        if (pumpVisualOff != null)
            pumpVisualOff.SetActive(!IsOn);
    }
}