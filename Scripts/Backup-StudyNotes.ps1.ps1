<#  -------------- 用户可自行修改的参数 -------------- #>
$NotesPath      = "C:\Users\24238\Documents\StudyNote"   # 要备份的文件或文件夹
$BackupRoot     = "D:\Data\DocsArchives\Backups-StudyNote"  # 备份根目录
$MaxBackups     = 7                                          # 最大保留份数
$ZipNamePrefix  = "StudyNote-"                                    # zip 文件名前缀
<#  --------------------------------------------------- #>

# 如果备份根目录不存在就创建
if (-not (Test-Path $BackupRoot)) {
    New-Item -Path $BackupRoot -ItemType Directory -Force | Out-Null
}

# 生成带时间戳的 zip 文件名
$timestamp   = Get-Date -Format "yyyy-MM-dd_HH-mm"
$zipFileName = "$ZipNamePrefix$timestamp.zip"
$zipFullPath = Join-Path $BackupRoot $zipFileName

# 压缩（支持文件或文件夹）
Compress-Archive -Path $NotesPath -DestinationPath $zipFullPath -CompressionLevel Optimal

# 计算当前已有备份数量
$existingBackups = Get-ChildItem -Path $BackupRoot -Filter "$ZipNamePrefix*.zip" |
                   Sort-Object LastWriteTime

$exceedCount = $existingBackups.Count - $MaxBackups

# 若超出最大备份数量，删除最旧的
if ($exceedCount -gt 0) {
    $existingBackups |
        Select-Object -First $exceedCount |
        Remove-Item -Force
}

# 可选：输出日志
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') Backup completed: $zipFullPath"