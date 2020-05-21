import shutil

file = open("grant_refs.txt", "r")

grant_refs = []

for each in file.readlines():
    grant_refs.append(each)


i = 0
for grant_ref in grant_refs:
    doc_name_ref = grant_ref.replace('/', '_')[:12]
    print(doc_name_ref)

    # DMP
    source_dmp = '/Users/qsp95418/Documents/datamad_docs/NE_H014756_1 DMP.pdf'
    destination_dmp = f'/Users/qsp95418/Documents/datamad_docs/{doc_name_ref} DMP.pdf'

    # CFS
    source_cfs = '/Users/qsp95418/Documents/datamad_docs/NE_G016909_1 CFS.pdf'
    destination_cfs = f'/Users/qsp95418/Documents/datamad_docs/{doc_name_ref} CFS.pdf'

    try:
        shutil.copy(source_dmp, destination_dmp)
        shutil.copy(source_cfs, destination_cfs)

    except shutil.SameFileError:
        pass

    i += 1

    if i > 999:
        break
