package it.interzen.zencommonlibrary.dto.zenprotocollo;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class CorrelatedProtocolDTO {

    private Long id;

    @Schema(description="The protocol number, must be unique and automatically generated. ", pattern="0000001")
    private String protocolNumber = null;

}
