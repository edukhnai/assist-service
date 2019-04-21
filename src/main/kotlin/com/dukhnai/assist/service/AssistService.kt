package com.dukhnai.assist.service

import org.springframework.stereotype.Service
import org.apache.logging.log4j.LogManager
import java.io.File

@Service
class AssistService {

    companion object {
        private val logger = LogManager.getLogger()
    }

    fun runAssistAlgorythm() {
        Runtime.getRuntime().exec("pip install pandas")
        val pb = ProcessBuilder("python", "assist.py").inheritIO()
        //pb.redirectOutput(ProcessBuilder.Redirect.appendTo(File("log.txt")))
        //pb.redirectError(ProcessBuilder.Redirect.appendTo(File("error.txt")))
        pb.start()
        logger.info("---------------------SCRIPT EXECUTED------------------------------")
        //logger.error(pb.)
    }
}