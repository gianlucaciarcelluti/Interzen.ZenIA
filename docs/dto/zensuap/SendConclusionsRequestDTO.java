package it.interzen.zencommonlibrary.dto.zensuap;

import lombok.Data;

@Data
public class SendConclusionsRequestDTO {
    Long documentId;
    EventEnum event;
    boolean sut = false;
}
