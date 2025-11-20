package it.interzen.zencommonlibrary.dto.zenprocess;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class TaskDTO {
	String id;
    String name;
    String description;
    Integer priority;
    String owner;
    String assignee;
    String processInstanceId;
    String executionId;
    String taskDefinitionId;
    String processDefinitionId;
    String scopeId;
    String subScopeId;
    String scopeType;
    String scopeDefinitionId;
    String propagatedStageInstanceId;
    String state;
    LocalDateTime createTime;
    LocalDateTime inProgressStartTime;
    String inProgressStartedBy;
    LocalDateTime claimTime;
    String claimedBy;
    Boolean isSuspended = false;
    LocalDateTime suspendedTime;
    String suspendedBy;
    String taskDefinitionKey;
    LocalDateTime inProgressStartDueDate;
    LocalDateTime dueDate;
    String category;
    String parentTaskId;
    String tenantId;
    String formKey;
    Integer processVersion;

    LocalDateTime endTime;
    String completedBy;
    Long durationInMillis;
    Long workTimeInMillis;
    
    Map<String, Object> taskLocalVariables;
    Map<String, Object> processVariables;
    Map<String, Object> caseVariables;

    // TODO: aggiungere con il converter
    List<HistoricIdentityLinkDTO> identityLinks;
}
