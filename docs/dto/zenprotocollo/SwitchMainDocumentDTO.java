package it.interzen.zencommonlibrary.dto.zenprotocollo;


import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class SwitchMainDocumentDTO {

    @NotNull
    private Long protocolId;

    @NotNull
    private Long newMainDocumentId;

    private Long oldMainDocumentId;

}
