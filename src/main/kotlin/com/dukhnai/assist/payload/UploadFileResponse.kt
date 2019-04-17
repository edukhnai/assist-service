package com.dukhnai.assist.payload

data class UploadFileResponse(
    private val filename: String,
    private val fileDownloadUri: String,
    private val fileType: String,
    private val size: Long
)