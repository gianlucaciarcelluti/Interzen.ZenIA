package it.interzen.zencommonlibrary.dto.zendocuments;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class DocumentFileDTO extends DocumentDTO {
	private Integer version;

	private Integer subVersion = 0;
	
	private String fileContentBase64;

	private String urlFile;
}
