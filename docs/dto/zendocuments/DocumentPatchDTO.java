package it.interzen.zencommonlibrary.dto.zendocuments;

import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.web.multipart.MultipartFile;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class DocumentPatchDTO  {
	@NotNull
	private Long id;

	@Enumerated(EnumType.STRING)
	protected DocumentStatus status;

	Long folderId;
}
