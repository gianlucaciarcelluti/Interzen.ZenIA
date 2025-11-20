package it.interzen.zencommonlibrary.dto.zenadmin;

import java.time.LocalDateTime;

import it.interzen.zencommonlibrary.dto.LookupElementDTOLong;
import it.interzen.zencommonlibrary.dto.TrackBasicChangesDTOHasID;
import it.interzen.zencommonlibrary.dto.ZenMicroservices;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
/**
 * @author Gianluca Lella
 */

@Data
@AllArgsConstructor
@NoArgsConstructor
public class SchedulerLogDTO  extends TrackBasicChangesDTOHasID<Long> {
	
	private Long id;
    private LookupElementDTOLong<SchedulerDTO> schedulerId; 
    private LocalDateTime requestDate;
    private ZenMicroservices requestMicroservices;
    private StatusSchedulerEnum schedulerStatus;
    private ResponseTypeEnum responseType;
    private String responseMessage;
    private String responseMessageCode;
    private String responseMessageDebug;
    private LocalDateTime responseTimestamp;
    private String responseData;

}
