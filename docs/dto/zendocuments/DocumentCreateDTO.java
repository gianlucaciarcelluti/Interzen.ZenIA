package it.interzen.zencommonlibrary.dto.zendocuments;

import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.web.multipart.MultipartFile;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class DocumentCreateDTO extends DocumentBaseDTO {
	@NotNull
	private MultipartFile file;
}
