package it.interzen.zencommonlibrary.dto.zendocuments;

import java.time.LocalDateTime;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class DocumentVersionDTO extends DocumentBaseDTO{
	private Integer version;

	private Integer subVersion = 0;

	private Long size;

	private LocalDateTime documentVersionDate;	
	
	private Long documentVersionOwner;
	
	
}
