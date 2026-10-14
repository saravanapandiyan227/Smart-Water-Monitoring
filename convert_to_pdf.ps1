$docPath = "C:\Users\SARAVANA PANDIYAN\Downloads\DEVOPS-PANDI\WaterMonitoring\Smart_Water_Monitoring_DevOps_Report.docx"
$pdfPath = "C:\Users\SARAVANA PANDIYAN\Downloads\DEVOPS-PANDI\WaterMonitoring\Smart_Water_Monitoring_DevOps_Report.pdf"

Write-Host "Starting Word Application..."
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    Write-Host "Opening $docPath..."
    $doc = $word.Documents.Open($docPath)
    Write-Host "Exporting to $pdfPath..."
    # 17 = wdFormatPDF
    $doc.SaveAs([ref]$pdfPath, [ref]17)
    $doc.Close()
    Write-Host "PDF successfully created!"
} catch {
    Write-Error $_
} finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
}
