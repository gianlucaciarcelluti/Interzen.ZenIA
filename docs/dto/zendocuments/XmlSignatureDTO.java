package it.interzen.zencommonlibrary.dto.zendocuments;

import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class XmlSignatureDTO {

	@NotNull
	private DocumentBaseDTO xmlSignatureDoc;
	
	@NotNull
	private Long protocolId;
	
	@NotNull
	private Long mainDocumentId;
	
	@NotNull
	private String xmlSignatureHeader;
	
	@NotNull
	private DocumentFlowTypeEnum flowType;
	
}
