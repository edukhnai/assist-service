package com.dukhnai.assist.controller

import com.dukhnai.assist.payload.UploadFileResponse
import com.dukhnai.assist.service.AssistService
import com.dukhnai.assist.service.FileStorageService
import org.springframework.core.io.Resource
import org.springframework.http.HttpHeaders
import org.springframework.http.MediaType
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*
import org.springframework.web.multipart.MultipartFile
import org.springframework.web.servlet.support.ServletUriComponentsBuilder
import javax.servlet.http.HttpServletRequest

@RestController
class FileController(
    private val fileStorageService: FileStorageService,
    private val assistService: AssistService
) {
    @PostMapping("/uploadFile")
    fun uploadFile(@RequestParam("file") file: MultipartFile): UploadFileResponse {
        val filename = fileStorageService.storeFile(file)

        val fileDownloadUri = ServletUriComponentsBuilder.fromCurrentContextPath()
            .path("/downloadFile/")
            .path(filename)
            .toUriString()

        return UploadFileResponse(filename, fileDownloadUri, file.contentType!!, file.size)
    }

    @GetMapping("/downloadFile/{filename:.+}")
    fun downloadFile(@PathVariable filename: String, request: HttpServletRequest): ResponseEntity<Resource> {
        val resource: Resource = fileStorageService.loadFile(filename)
        var contentType = request.servletContext.getMimeType(resource.file.absolutePath)
        if (contentType == null) {
            contentType = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        }

        //assistService.runAssistAlgorithm()

        return ResponseEntity.ok()
            .contentType(MediaType.parseMediaType(contentType))
            .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"${resource.filename}\"")
            .body(resource)
    }
}