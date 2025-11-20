package it.interzen.zencommonlibrary.dto.zenprotocollo;

import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Map;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class ProtocolDocumentDataDTO {

    @NotNull private Long protocolId;
    @NotNull private String description;
    @NotNull private String fileName;
    private String barCode;
    private String externalReference;
    private String note;
}
