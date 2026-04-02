using UnityEditor;
using UnityEngine;
using UnityEditor.Build.Reporting;

public class BuildScript
{
    [MenuItem("Build/Build Windows")]
    public static void BuildWindows()
    {
        string buildPath = "Builds/Windows/MyPalletizerSimulation.exe";
        BuildPlayerOptions buildPlayerOptions = new BuildPlayerOptions();
        buildPlayerOptions.scenes = new[] { "Assets/Scenes/SampleScene.unity" };
        buildPlayerOptions.locationPathName = buildPath;
        buildPlayerOptions.target = BuildTarget.StandaloneWindows64;
        buildPlayerOptions.options = BuildOptions.None;

        BuildReport report = BuildPipeline.BuildPlayer(buildPlayerOptions);
        BuildSummary summary = report.summary;

        if (summary.result == BuildResult.Succeeded)
        {
            Debug.Log("Build succeeded: " + (summary.totalSize / 1024 / 1024) + " MB");
        }

        if (summary.result == BuildResult.Failed)
        {
            Debug.LogError("Build failed");
        }
    }

    [MenuItem("Build/Build Linux")]
    public static void BuildLinux()
    {
        string buildPath = "Builds/Linux/MyPalletizerSimulation.x86_64";
        BuildPlayerOptions buildPlayerOptions = new BuildPlayerOptions();
        buildPlayerOptions.scenes = new[] { "Assets/Scenes/SampleScene.unity" };
        buildPlayerOptions.locationPathName = buildPath;
        buildPlayerOptions.target = BuildTarget.StandaloneLinux64;
        buildPlayerOptions.options = BuildOptions.None;

        BuildReport report = BuildPipeline.BuildPlayer(buildPlayerOptions);
        BuildSummary summary = report.summary;

        if (summary.result == BuildResult.Succeeded)
        {
            Debug.Log("Build succeeded: " + (summary.totalSize / 1024 / 1024) + " MB");
        }

        if (summary.result == BuildResult.Failed)
        {
            Debug.LogError("Build failed");
        }
    }
}
