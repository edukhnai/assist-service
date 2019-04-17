import com.dukhnai.assist.controller.AssistController
import org.junit.Test
import org.springframework.http.HttpEntity
import org.springframework.http.HttpHeaders
import org.springframework.http.HttpMethod
import org.springframework.http.MediaType
import org.springframework.web.client.RestTemplate
import java.nio.charset.StandardCharsets
import java.io.FileOutputStream

class InterestingTests {

   // @Test
    fun `loads pdf file from the specified uri`() {
        val url = "https://imwerden.de/pdf/bocharov_roman_tolstogo_vojna_i_mir_1978__ocr.pdf"

        val out = FileOutputStream("out.pdf")
        out.write(loadFileWithRestTemplate(url))
        out.close()
    }

    private fun loadFileWithRestTemplate(webLink: String): ByteArray? {
        val restTemplate = RestTemplate()
        val httpHeaders = HttpHeaders()
        httpHeaders.acceptCharset = listOf(StandardCharsets.UTF_8)
        httpHeaders.connection = listOf("Keep-Alive")
        httpHeaders.cacheControl = "no-cache"
        httpHeaders.contentType = MediaType.MULTIPART_FORM_DATA

        val httpEntity = HttpEntity<ByteArray?>(httpHeaders)
        val responseEntity = restTemplate
            .exchange(webLink, HttpMethod.POST, httpEntity, ByteArray::class.java)

        return responseEntity.body
    }

}