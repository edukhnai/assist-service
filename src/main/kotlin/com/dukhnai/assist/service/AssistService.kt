package com.dukhnai.assist.service

import org.springframework.stereotype.Service

@Service
class AssistService {

    fun runAssistAlgorythm() {
        Runtime.getRuntime().exec("python assist.py")
        Thread.sleep(1000)
    }
}