package com.dukhnai.assist.controller

import com.dukhnai.assist.dto.Assist
import com.dukhnai.assist.dto.Timetable
import com.dukhnai.assist.payload.UploadFileResponse
import com.dukhnai.assist.service.FileStorageService
import com.fasterxml.jackson.databind.ObjectMapper
import org.springframework.core.io.Resource
import org.springframework.http.HttpHeaders
import org.springframework.http.MediaType
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*
import org.springframework.web.multipart.MultipartFile
import org.springframework.web.servlet.support.ServletUriComponentsBuilder
import java.nio.file.Files
import java.nio.file.Paths
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

         return UploadFileResponse(filename, fileDownloadUri, file.contentType!!, file.size)
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

    @GetMapping( "/timetable-by-fio")
    fun getTimetableByFio(
        @RequestParam("first-name") firstName: String,
        @RequestParam("last-name") lastName: String
    ): Assist {
        return getAssistByFio("$lastName $firstName")
    }

    private fun getAssistByFio(fio: String): Assist {
        val objectMapper = ObjectMapper()
        val initialData = Files.readAllBytes(Paths.get("data_file.json"))
        val timetable = objectMapper.readValue(initialData, Timetable::class.java)

        for (assist in timetable.assists) {
            if (fio == assist.assistant) {
                return assist
            }
        }

        return Assist("No assistant found", emptyList())
    }
}