param(
    [Parameter(Mandatory = $true)][string]$PrinterName,
    [Parameter(Mandatory = $true)][string]$FilePath
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $FilePath)) {
    Write-Error "Receipt file not found."
    exit 1
}

$bytes = [System.IO.File]::ReadAllBytes($FilePath)
if ($bytes.Length -eq 0) {
    Write-Error "Receipt is empty."
    exit 1
}

Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public class PbccRawPrinter {
    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi)]
    public class DOCINFOA {
        [MarshalAs(UnmanagedType.LPStr)] public string pDocName;
        [MarshalAs(UnmanagedType.LPStr)] public string pOutputFile;
        [MarshalAs(UnmanagedType.LPStr)] public string pDataType;
    }
    [DllImport("winspool.drv", CharSet = CharSet.Ansi, SetLastError = true)]
    public static extern bool OpenPrinter(string szPrinter, out IntPtr hPrinter, IntPtr pd);
    [DllImport("winspool.drv", SetLastError = true)]
    public static extern bool ClosePrinter(IntPtr hPrinter);
    [DllImport("winspool.drv", CharSet = CharSet.Ansi, SetLastError = true)]
    public static extern bool StartDocPrinter(IntPtr hPrinter, int level, [In] DOCINFOA di);
    [DllImport("winspool.drv", SetLastError = true)]
    public static extern bool EndDocPrinter(IntPtr hPrinter);
    [DllImport("winspool.drv", SetLastError = true)]
    public static extern bool StartPagePrinter(IntPtr hPrinter);
    [DllImport("winspool.drv", SetLastError = true)]
    public static extern bool EndPagePrinter(IntPtr hPrinter);
    [DllImport("winspool.drv", SetLastError = true)]
    public static extern bool WritePrinter(IntPtr hPrinter, IntPtr pBytes, int dwCount, out int dwWritten);
}
"@

$handle = [IntPtr]::Zero
if (-not [PbccRawPrinter]::OpenPrinter($PrinterName, [ref]$handle, [IntPtr]::Zero)) {
    Write-Error "Could not open printer $PrinterName."
    exit 2
}

$doc = New-Object PbccRawPrinter+DOCINFOA
$doc.pDocName = "Library receipt"
$doc.pDataType = "RAW"
$doc.pOutputFile = $null

if (-not [PbccRawPrinter]::StartDocPrinter($handle, 1, $doc)) {
    [PbccRawPrinter]::ClosePrinter($handle) | Out-Null
    Write-Error "Could not start print job."
    exit 3
}

if (-not [PbccRawPrinter]::StartPagePrinter($handle)) {
    [PbccRawPrinter]::EndDocPrinter($handle) | Out-Null
    [PbccRawPrinter]::ClosePrinter($handle) | Out-Null
    Write-Error "Could not start print page."
    exit 4
}

$pointer = [System.Runtime.InteropServices.Marshal]::AllocHGlobal($bytes.Length)
[System.Runtime.InteropServices.Marshal]::Copy($bytes, 0, $pointer, $bytes.Length)
$written = 0
$wrote = [PbccRawPrinter]::WritePrinter($handle, $pointer, $bytes.Length, [ref]$written)
[System.Runtime.InteropServices.Marshal]::FreeHGlobal($pointer)

[PbccRawPrinter]::EndPagePrinter($handle) | Out-Null
[PbccRawPrinter]::EndDocPrinter($handle) | Out-Null
[PbccRawPrinter]::ClosePrinter($handle) | Out-Null

if (-not $wrote) {
    Write-Error "Could not write receipt."
    exit 5
}

exit 0
