package com.dukhnai.assist

import com.dukhnai.assist.property.FileStorageProperties
import org.springframework.boot.SpringApplication
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.context.properties.EnableConfigurationProperties

@SpringBootApplication
@EnableConfigurationProperties(FileStorageProperties::class)
open class AssistApplication

fun main(args: Array<String>) {
    SpringApplication.run(AssistApplication::class.java, *args)
}