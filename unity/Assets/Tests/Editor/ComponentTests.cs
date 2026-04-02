using NUnit.Framework;
using UnityEngine;

public class ComponentTests
{
    [Test]
    public void ArticulationJointActuator_RequiresArticulationBody()
    {
        var go = new GameObject("TestActuator");
        var actuator = go.AddComponent<ArticulationJointActuator>();
        
        var body = go.GetComponent<ArticulationBody>();
        
        Assert.IsNotNull(actuator, "Actuator should be added");
        Assert.IsNotNull(body, "ArticulationBody should be automatically added due to RequireComponent");
    }

    [Test]
    public void WorldSpawnManager_Defaults()
    {
        var go = new GameObject("SpawnManager");
        var manager = go.AddComponent<WorldSpawnManager>();
        
        Assert.IsNull(manager.boxPrefab);
        Assert.IsNull(manager.spherePrefab);
        Assert.IsNull(manager.cylinderPrefab);
    }
}
