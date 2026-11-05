param(
	[ValidateSet('ac5', 'ac6')]
	[string]$Variant = 'ac6'
)

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..\..')).Path
$sourceProject = Join-Path $repoRoot 'KEIL_PRJ\MM32SPIN0230_Demo.uvprojx'
$sourceProjectDir = Split-Path -Parent $sourceProject
$outputRoot = Join-Path $PSScriptRoot $Variant
$null = New-Item -ItemType Directory -Path $outputRoot -Force
$null = New-Item -ItemType Directory -Path (Join-Path $outputRoot 'Objects') -Force
$null = New-Item -ItemType Directory -Path (Join-Path $outputRoot 'Listings') -Force
[xml]$project = Get-Content -LiteralPath $sourceProject -Raw

foreach ($node in $project.SelectNodes('//FilePath | //ScatterFile'))
{
	if ($node.InnerText -and -not [IO.Path]::IsPathRooted($node.InnerText))
	{
		$node.InnerText = [IO.Path]::GetFullPath((Join-Path $sourceProjectDir $node.InnerText))
	}
}
foreach ($node in $project.SelectNodes('//IncludePath'))
{
	if ($node.InnerText)
	{
		$node.InnerText = (($node.InnerText -split ';' | ForEach-Object {
			if ([IO.Path]::IsPathRooted($_)) { $_ }
			else { [IO.Path]::GetFullPath((Join-Path $sourceProjectDir $_)) }
		}) -join ';')
	}
}
$target = $project.Project.Targets.Target
$target.TargetOption.TargetCommonOption.OutputDirectory = (Join-Path $outputRoot 'Objects') + '\'
$target.TargetOption.TargetCommonOption.ListingPath = (Join-Path $outputRoot 'Listings') + '\'
if ($Variant -eq 'ac6')
{
	$target.uAC6 = '1'
	$target.pArmCC = '6220000::V6.22::ARMCLANG'
	$target.pCCUsed = '6220000::V6.22::ARMCLANG'
}
$buildProject = Join-Path $outputRoot 'MM32SPIN0230_Demo.uvprojx'
$project.Save($buildProject)
$buildLog = Join-Path $outputRoot 'rebuild.log'
$uv4Path = 'D:\Users\mym02\AppData\Local\Keil_v5\UV4\UV4.exe'
$uv4Args = '-r "' + $buildProject + '" -t "MM32SPIN0230" -o "' + $buildLog + '"'
$started = [DateTime]::UtcNow
$process = Start-Process -FilePath $uv4Path -ArgumentList $uv4Args -WindowStyle Hidden -PassThru -Wait
if (Test-Path -LiteralPath $buildLog)
{
	Get-Content -LiteralPath $buildLog | Select-Object -Last 35
}
$axf = Join-Path $outputRoot 'Objects\SPIN0230_DEMO.axf'
$hex = Join-Path $outputRoot 'Objects\SPIN0230_DEMO.hex'
Write-Output ('UV4 exit code: ' + $process.ExitCode)
foreach ($artifact in @($axf, $hex))
{
	if (-not (Test-Path -LiteralPath $artifact)) { throw ('Missing artifact: ' + $artifact) }
	$item = Get-Item -LiteralPath $artifact
	if ($item.LastWriteTimeUtc -lt $started) { throw ('Stale artifact: ' + $artifact) }
	Write-Output ($item.FullName + ' : ' + $item.Length + ' bytes')
}
if ($process.ExitCode -gt 1) { throw ('Build failed: ' + $process.ExitCode) }
