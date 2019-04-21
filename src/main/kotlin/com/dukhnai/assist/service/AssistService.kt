package com.dukhnai.assist.service

import org.springframework.stereotype.Service

@Service
class AssistService {

    fun runAssistAlgorithm() {
        ProcessBuilder("python", "assist.py").inheritIO().start()
    }
}