package it.interzen.zencommonlibrary.dto.zenprocess;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

import java.util.Date;
import java.util.Map;

@Data
@EqualsAndHashCode(callSuper = false)
@AllArgsConstructor
@NoArgsConstructor
public class HistoricProcessInstanceDTO {
	String id;
	String businessKey;
	String businessStatus;
	String processDefinitionId;
	String processDefinitionName;
	String processDefinitionKey;
	String processDefinitionVersion;
	String processDefinitionCategory;
	boolean completed = false;
	String deploymentId;
	Date startTime;
	Date endTime;
	Long durationInMillis;
	String endActivityId;
	String startUserId;
	String startActivityId;
	String deleteReason;
	String superProcessInstanceId;
	String tenantId;
	String description;
	String callbackId;
	String callbackType;
	String referenceId;
	String referenceType;
	String propagatedStageInstanceId;
	Map<String, Object> processVariables;
}
