package it.interzen.zencommonlibrary.dto.zensuap;

import lombok.Data;

@Data
public class IntegrationRequestDTO {
    Long documentId;
    String integrationRequest;
    boolean sut = false;
}
