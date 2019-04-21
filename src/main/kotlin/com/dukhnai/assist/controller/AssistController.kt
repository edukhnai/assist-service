package com.dukhnai.assist.controller

import com.dukhnai.assist.dto.Assist
import com.dukhnai.assist.dto.Timetable
import com.dukhnai.assist.service.AssistService
import com.fasterxml.jackson.databind.ObjectMapper
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestParam
import org.springframework.web.bind.annotation.RestController
import java.io.File
import java.nio.file.Files
import java.nio.file.Paths

@RestController
class AssistController(val assistService: AssistService) {

    @GetMapping( "/timetable-by-fio")
    fun getTimetableByFio(
        @RequestParam("first-name") firstName: String,
        @RequestParam("last-name") lastName: String
    ): Assist {
        val fio = "$lastName $firstName"
        val objectMapper = ObjectMapper()

        assistService.runAssistAlgorithm()

        val tempFile = File("data_file.json")
        if (!tempFile.exists()) {
            throw RuntimeException("File was not created")
        }

        val resultData = Files.readAllBytes(Paths.get("data_file.json"))
        val timetable = objectMapper.readValue(resultData, Timetable::class.java)

        for (assist in timetable.assists) {
            if (fio == assist.assistant) {
                return assist
            }
        }

        return Assist("Assistant not found", emptyList())
    }
}