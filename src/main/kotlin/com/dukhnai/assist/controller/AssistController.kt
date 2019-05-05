package com.dukhnai.assist.controller

import com.dukhnai.assist.dto.Assist
import com.dukhnai.assist.dto.Timetable
import com.fasterxml.jackson.databind.ObjectMapper
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestParam
import org.springframework.web.bind.annotation.RestController
import java.nio.file.Files
import java.nio.file.Paths

@RestController
class AssistController {

    @GetMapping("/timetable-by-fio")
    fun getTimetableByFio(
        @RequestParam("first-name") firstName: String,
        @RequestParam("last-name") lastName: String
    ): Assist {
        val fio = "$lastName $firstName"
        val objectMapper = ObjectMapper()

        val resultData = Files.readAllBytes(Paths.get("data_file.json"))
        val timetable = objectMapper.readValue(resultData, Timetable::class.java)

        for (assist in timetable.assists) {
            if (fio == assist.assistant) {
                return assist
            }
        }

        return Assist("Assistant not found", emptyList())
    }

    @GetMapping("/all-timetables")
    fun getAllTimetables(): List<Assist> {
        val assists = mutableListOf<Assist>()

        val objectMapper = ObjectMapper()

        val resultData = Files.readAllBytes(Paths.get("data_file.json"))
        val timetable = objectMapper.readValue(resultData, Timetable::class.java)

        for (assist in timetable.assists) {
            assists.add(assist)
        }
        return assists
    }
}
