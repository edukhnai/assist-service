package com.dukhnai.assist.controller

import com.dukhnai.assist.payload.UploadFileResponse
import com.dukhnai.assist.property.FileStorageProperties
import com.dukhnai.assist.service.FileStorageService
import org.springframework.boot.context.properties.EnableConfigurationProperties
import org.springframework.core.io.Resource
import org.springframework.http.HttpHeaders
import org.springframework.http.MediaType
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestParam
import org.springframework.web.bind.annotation.RestController
import org.springframework.web.multipart.MultipartFile
import org.springframework.web.servlet.support.ServletUriComponentsBuilder
import javax.servlet.http.HttpServletRequest

@RestController
class AssistController(private val fileStorageService: FileStorageService) {

    @PostMapping("/uploadFile")
    fun uploadFile(@RequestParam("file") file: MultipartFile): UploadFileResponse {
        val filename = fileStorageService.storeFile(file)

        val fileDownloadUri = ServletUriComponentsBuilder.fromCurrentContextPath()
            .path("/downloadFile/")
            .path(filename)
            .toUriString()

         return UploadFileResponse(filename, fileDownloadUri, file.contentType, file.size)
    }

    @GetMapping("/downloadFile/{filename:.+}")
    fun downloadFile(@PathVariable filename: String, request: HttpServletRequest): ResponseEntity<Resource> {
        val resource: Resource = fileStorageService.loadFile(filename)
        val contentType = request.servletContext.getMimeType(resource.file.absolutePath)

        return ResponseEntity.ok()
            .contentType(MediaType.parseMediaType(contentType))
            .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"${resource.filename}\"")
            .body(resource)
    }
}