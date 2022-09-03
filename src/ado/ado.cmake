set(ado_base_dir ${CMAKE_CURRENT_LIST_DIR})

function (ado_add_schema project_ref out_var in_path)

  file(RELATIVE_PATH schema_path       ${abs_src} ${in_path})
  file(RELATIVE_PATH manifest_rel_path ${abs_src} ${in_path}-manifest)
  set(manifest_abs_path "${abs_gen}/${manifest_rel_path}")
  
  if (NOT (EXISTS ${manifest_abs_path}))
    message(STATUS "Parsing ${schema_path}")
	
    execute_process(
      COMMAND ${Python3_EXECUTABLE}
              ${ado_base_dir}/parse_schema.py ${python_paths}
              ${in_path} ${manifest_abs_path}
			  --manifest_only
    )
  endif()
  set_property(DIRECTORY APPEND PROPERTY CMAKE_CONFIGURE_DEPENDS ${manifest_abs_path})
  
  file(STRINGS ${manifest_abs_path} manifest_data)

  while (manifest_data)
    list(POP_FRONT manifest_data line)

    if (line MATCHES "^gen: .*")
      string(SUBSTRING ${line} 5 -1 line)
      list(APPEND out_gen     ${line})
      list(APPEND out_gen_str ${abs_gen}/${line})
    endif()
    if (line MATCHES "^def: .*")
      string(SUBSTRING ${line} 5 -1 line)
      list(APPEND out_src ${line})
    endif()
  endwhile()
  
  list(APPEND out_gen ${manifest_rel_path})
      
  add_custom_command(
    COMMENT "Processing Ado schema ${schema_path}"
    OUTPUT  ${out_gen_str}
    COMMAND ${Python3_EXECUTABLE}
            ${ado_base_dir}/parse_schema.py ${python_paths}
            ${in_path} ${manifest_abs_path}
    DEPENDS ${ado_base_dir}/parse_schema.py
            ${in_path}
    VERBATIM
  )

  set(${out_var}_gen ${out_gen} PARENT_SCOPE)
  set(${out_var}_src ${out_src} PARENT_SCOPE)
  
endfunction()