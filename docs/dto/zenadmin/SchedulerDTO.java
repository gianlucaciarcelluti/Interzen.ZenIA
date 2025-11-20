package it.interzen.zencommonlibrary.dto.zenadmin;

import java.time.LocalDateTime;
import java.time.LocalTime;
import it.interzen.zencommonlibrary.dto.TrackBasicChangesDTOHasID;
import it.interzen.zencommonlibrary.dto.ZenMicroservices;
import it.interzen.zencommonlibrary.dto.zenscheduler.BusEnum;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;


/**
 * @author Gianluca Lella
 */

@Data
@AllArgsConstructor
@NoArgsConstructor
public class SchedulerDTO extends TrackBasicChangesDTOHasID<Long> {
    
    private Long id;
    private String description;
    private String code;
    private Boolean active=false;
    private ZenMicroservices microservices;
    private String classMicroservice;
    private String methodMicroservice;
    private String parametersMicroservice;
    private Integer frequency;
    private LocalTime fromTime;
    private LocalTime toTime;
    private Boolean weekday1=false;
    private Boolean weekday2=false;
    private Boolean weekday3=false;
    private Boolean weekday4=false;
    private Boolean weekday5=false;
    private Boolean weekday6=false;
    private Boolean weekday7=false;
    private StatusSchedulerEnum lastStatus;
    private String lastError;
    private LocalDateTime lastExecutionDate;
    private BusEnum typeBus;
}