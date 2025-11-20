package it.interzen.zencommonlibrary.dto.zenprotocollo;

import java.time.LocalDate;
import java.time.LocalDateTime;

import it.interzen.zencommonlibrary.crud_base.HasID;
import it.interzen.zencommonlibrary.dto.LookupElementDTOString;
import it.interzen.zencommonlibrary.dto.TrackBasicChangesDTO;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class SpecialRegisterSummaryDTO extends TrackBasicChangesDTO implements HasID<Long> {
    private Long id;
	
	private Long aooid;
	
	private Integer year = LocalDate.now().getYear();
	
    private LookupElementDTOString<SpecialRegisterTypeDTO> registryCode;
    
    private RegisterStatus registerStatus = RegisterStatus.OPEN;
    
    @NotNull
	private LocalDateTime closedDate;
    
	private Long summaryDocumentId;
    
	private Long totalEvents;
}
