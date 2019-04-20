package com.dukhnai.assist.dto

data class Assist(
    val assistant: String = "",
    val pairs: List<String> = emptyList()
)