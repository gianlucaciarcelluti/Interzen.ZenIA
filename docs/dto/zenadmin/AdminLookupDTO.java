package it.interzen.zencommonlibrary.dto.zenadmin;
import lombok.*;
import org.springframework.web.multipart.MultipartFile;

import it.interzen.zencommonlibrary.dto.TrackBasicChangesDTOHasID;
import it.interzen.zencommonlibrary.dto.zendocuments.DocumentCreateDTO;


@Data
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(callSuper = true)
public class AdminLookupDTO extends TrackBasicChangesDTOHasID<Long> {

	private Long id;
	private String description;
	private String code;
	private String tablename;
	private Boolean active = true;
}