package it.interzen.zencommonlibrary.dto.zenprocess;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.NonNull;

import java.util.Map;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class HttpRequestDTO {
    @NonNull
    String url;
    String method = "GET"; // Default to GET if not specified
    String headersJson;
    String body;
    String queryParamsJson;
    String statusCodeVar;
    String responseBodyVar;
    String errorVar;
    // se presente, contiene le colonne (come valori della mappa) da inserire
    // nella risposta rinominate (con le chiavi della mappa)
    Map<String, String> columns;
}
