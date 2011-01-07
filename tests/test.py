from OpenPanel.exception import CoreException

def test(ctx):
    """run dbmanager tests. relies on Domain.module. leaves a Domain object behind."""
    dom1 = ctx.prefix+'dom1.example.com'
    ctx.domain = dom1
    doms = ctx.conn.rpc.getrecords(classid="Domain")
    if dom1 in doms['body']['data'].get('Domain',{}).keys():
        ctx.fail("domain-already-exists", "found Domain %s before create" % dom1)
        return False
    dom1id = ctx.conn.rpc.create(classid="Domain", objectid=dom1)['body']['data']['objid']
    ctx.logger.debug('created Domain %s (%s)' % (dom1, dom1id))

    doms = ctx.conn.rpc.getrecords(classid="Domain")

    if dom1 not in doms['body']['data'].get('Domain',{}).keys():
        ctx.fail("domain-not-created", "did not find Domain %s after create" % dom1)
        return False

    doms = ctx.conn.rpc.getrecords(classid="Domain")
    if doms['body']['data']['Domain'][dom1]['uuid'] != dom1id:
        ctx.fail("uuid-mismatch", "UUID mismatch for %s (%s!=%s)" % (
            dom1,
            doms['body']['data']['Domain'][dom1]['uuid']))
        return False

    ctx.conn.rpc.delete(classid="Domain", objectid=dom1)
    ctx.logger.debug("deleted Domain %s by name" % dom1)

    doms = ctx.conn.rpc.getrecords(classid="Domain")
    if dom1 in doms['body']['data'].get('Domain',{}).keys():
        ctx.fail("domain-not-deleted", "found Domain %s after delete/before new create" % dom1)
        return False
    dom1id2 = ctx.conn.rpc.create(classid="Domain", objectid=dom1)['body']['data']['objid']
    ctx.logger.debug('created Domain %s (%s)' % (dom1, dom1id2))
    if dom1id == dom1id2:
        ctx.fail("uuid-reuse", "UUID reuse detected")
        return False

    doms = ctx.conn.rpc.getrecords(classid="Domain")

    if dom1 not in doms['body']['data'].get('Domain',{}).keys():
        ctx.fail("domain-not-created-2", "did not find Domain %s after create" % dom1)
        return False

    doms = ctx.conn.rpc.getrecords(classid="Domain")
    if doms['body']['data']['Domain'][dom1]['uuid'] != dom1id2:
        ctx.fail("uuid-mismatch-2", "UUID mismatch for %s (%s!=%s)" % (
            dom1,
            doms['body']['data']['Domain'][dom1]['uuid']))
        return False

    ctx.conn.rpc.delete(classid="Domain", objectid=dom1id2)
    ctx.logger.debug("deleted Domain %s by uuid" % dom1)

    doms = ctx.conn.rpc.getrecords(classid="Domain")
    if dom1 in doms['body']['data'].get('Domain',{}).keys():
        ctx.fail("domain-not-deleted-2", "found Domain %s after delete" % dom1)
        return False

    dom1id3 = ctx.conn.rpc.create(classid="Domain", objectid=dom1)['body']['data']['objid']
    ctx.domainuuid=dom1id3
    ctx.logger.debug('created Domain %s (%s)' % (dom1, dom1id))
    success=False
    try:
        dom1id3b = ctx.conn.rpc.create(classid="Domain", objectid=dom1)['body']['data']['objid']
    except CoreException:
        success=True
    ctx.logger.debug('create Domain %s correctly refused' % (dom1))
    
    return True

def cleanup(ctx):
    ctx.conn.rpc.delete(classid="Domain", objectid=ctx.domain)
    ctx.logger.debug("deleted Domain %s by name" % ctx.domain)
    return True
