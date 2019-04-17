package com.dukhnai.assist.service

import com.dukhnai.assist.property.FileStorageProperties
import org.springframework.core.io.Resource
import org.springframework.core.io.UrlResource
import org.springframework.stereotype.Service
import org.springframework.util.StringUtils
import org.springframework.web.multipart.MultipartFile
import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths
import java.nio.file.StandardCopyOption

@Service
class FileStorageService(private val fileStorageProperties: FileStorageProperties) {//???

    private val fileLocation: Path = Paths.get(fileStorageProperties.uploadDir)
        .toAbsolutePath()
        .normalize()//как добавить проперть в конструктор?

    init {
        Files.createDirectories(fileLocation)
    }

    fun storeFile(file: MultipartFile): String {
        val filename = StringUtils.cleanPath(file.originalFilename)
        val targetLocation = fileLocation.resolve(filename)
        Files.copy(file.inputStream, targetLocation, StandardCopyOption.REPLACE_EXISTING)
        return filename
    }

    fun loadFile(filename: String): Resource {
        val filePath = fileLocation.resolve(filename).normalize()
        val resource = UrlResource(filePath.toUri())
        if (resource.exists()) {
            return resource
        } else {
            throw RuntimeException("file $filename not found")
        }
    }
}