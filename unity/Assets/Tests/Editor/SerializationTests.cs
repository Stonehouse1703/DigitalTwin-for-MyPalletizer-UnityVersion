using NUnit.Framework;
using UnityEngine;
using System;

public class SerializationTests
{
    [Test]
    public void WorldMessage_Serialization_Success()
    {
        string json = "{\"v\": 1, \"type\": \"spawn\", \"object_type\": \"box\", \"name\": \"box1\", \"position\": {\"x\": 1.5, \"y\": 2.5, \"z\": 3.5}}";
        var msg = JsonUtility.FromJson<WorldMessage>(json);

        Assert.AreEqual(1, msg.v);
        Assert.AreEqual("spawn", msg.type);
        Assert.AreEqual("box", msg.object_type);
        Assert.AreEqual("box1", msg.name);
        Assert.IsNotNull(msg.position);
        Assert.AreEqual(1.5f, msg.position.x);
        Assert.AreEqual(2.5f, msg.position.y);
        Assert.AreEqual(3.5f, msg.position.z);
    }

    [Test]
    public void WorldMessage_MissingFields_ReturnsDefaults()
    {
        string json = "{\"type\": \"clear\"}";
        var msg = JsonUtility.FromJson<WorldMessage>(json);

        Assert.AreEqual(0, msg.v); // default int
        Assert.AreEqual("clear", msg.type);
        Assert.IsNull(msg.name); // default string is null or empty depending on Unity's JsonUtility
        Assert.IsNull(msg.position); // reference type defaults to null
    }

    [Test]
    public void RobotData_Serialization_Full()
    {
        string json = "{" +
                      "\"type\": \"move_joints\"," +
                      "\"j1\": 10.5," +
                      "\"j2\": -20.0," +
                      "\"j3\": 30.1," +
                      "\"j4\": 45.0," +
                      "\"speed\": 100," +
                      "\"r\": 255, \"g\": 0, \"b\": 128," +
                      "\"tool\": \"gripper\"," +
                      "\"flag\": 1," +
                      "\"type_1\": 0," +
                      "\"enabled\": true" +
                      "}";
        var data = JsonUtility.FromJson<UnityUdpBridge.RobotData>(json);

        Assert.AreEqual("move_joints", data.type);
        Assert.AreEqual(10.5f, data.j1);
        Assert.AreEqual(-20.0f, data.j2);
        Assert.AreEqual(30.1f, data.j3);
        Assert.AreEqual(45.0f, data.j4);
        Assert.AreEqual(100, data.speed);
        Assert.AreEqual(255, data.r);
        Assert.AreEqual(0, data.g);
        Assert.AreEqual(128, data.b);
        Assert.AreEqual("gripper", data.tool);
        Assert.AreEqual(1, data.flag);
        Assert.AreEqual(0, data.type_1);
        Assert.IsTrue(data.enabled);
    }

    [Test]
    public void ColorData_Serialization_Success()
    {
        string json = "{\"r\": 255, \"g\": 128, \"b\": 0}";
        var color = JsonUtility.FromJson<ColorData>(json);

        Assert.IsNotNull(color);
        Assert.AreEqual(255, color.r);
        Assert.AreEqual(128, color.g);
        Assert.AreEqual(0, color.b);
    }
}
