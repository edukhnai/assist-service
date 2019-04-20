package com.dukhnai.assist.service

import org.springframework.stereotype.Service
import org.apache.logging.log4j.LogManager

@Service
class AssistService {

    companion object {
        private val logger = LogManager.getLogger()
    }

    fun runAssistAlgorythm() {
        Runtime.getRuntime().exec("python assist.py")
        logger.info("---------------------SCRIPT EXECUTED------------------------------")
        Thread.sleep(1000)
    }
}