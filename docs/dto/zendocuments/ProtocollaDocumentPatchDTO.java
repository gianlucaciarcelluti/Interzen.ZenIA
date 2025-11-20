package it.interzen.zencommonlibrary.dto.zendocuments;

import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ProtocollaDocumentPatchDTO {

    @NotNull
    private Long id;

    @NotNull
    private Long folderId;

    @NotNull
    @Enumerated(EnumType.STRING)
    protected DocumentStatusRegistration statusRegistration;

}
