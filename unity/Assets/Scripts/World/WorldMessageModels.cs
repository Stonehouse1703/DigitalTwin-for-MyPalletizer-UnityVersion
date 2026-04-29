using System;

[Serializable]
public class Vec3Data
{
    public float x;
    public float y;
    public float z;
}

[Serializable]
public class ColorData
{
    public int r;
    public int g;
    public int b;
}

[Serializable]
public class WorldMessage
{
    public int v;
    public string type;
    public string object_type;
    public string name;
    public Vec3Data position;
    public Vec3Data rotation;
    public Vec3Data scale;
    public ColorData color;
    public bool is_static;
}