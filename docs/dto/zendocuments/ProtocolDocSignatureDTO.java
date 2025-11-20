package it.interzen.zencommonlibrary.dto.zendocuments;

import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ProtocolDocSignatureDTO {

    // Solo uno dei 2 campi deve essere valorizzato
    private Long documentId;
    private String docToken;

    @NotNull
    private String base64Watermark;

    @NotNull
    private float watermarkPositionX;

    @NotNull
    private float watermarkPositionY;
    
    private Integer watermarkWidth;
	
	private Integer watermarkHeight;

}
